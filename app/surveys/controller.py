from datetime import datetime

from fastapi import HTTPException
from psycopg2 import IntegrityError
from app.common.database import cursor
from app.surveys.schema import SurveyCreateSchema, SurveyOptionSchema, SurveyQuestionSchema, SurveyQuestionTypeSchema


def create_survey_controller(body: SurveyCreateSchema):
    try:

        created_at = datetime.now()
        updated_at = datetime.now()
        query = """
        INSERT INTO survey (title,description,created_at,updated_at,is_active)
        VALUES (%s,%s,%s,%s,%s) RETURNING *;
        """
        params = (
            body.title,
            body.description,
            created_at,
            updated_at,
            body.is_active
        )
        cursor.execute(query, params)
        new_survey = cursor.fetchone()
        cursor.connection.commit()
        return {"survey": new_survey}
    except Exception as e:
        cursor.connection.rollback()
        raise RuntimeError(f"Error creating survey: {str(e)}")


def create_survey_question_controller(survey_id: int, body: SurveyQuestionSchema):
    try:

        survey_check_query = "SELECT * FROM survey WHERE id = %s;"
        cursor.execute(survey_check_query, (survey_id,))
        survey_exists = cursor.fetchone()
        if not survey_exists:
            raise RuntimeError(f"La encuesta con id {survey_id} no existe.")
        question_type_check_query = "SELECT * FROM question_type WHERE id= %s;"
        cursor.execute(question_type_check_query, (body.id_question_type,))
        question_type_exists = cursor.fetchone()
        if not question_type_exists:
            raise RuntimeError(
                f"El tipo de pregunta con id {body.id_question_type} no existe.")

        created_at = datetime.now()
        updated_at = datetime.now()
        query = """
        INSERT INTO question(survey_id,id_question_type ,text,created_at,updated_at,is_active)
        VALUES (%s,%s,%s,%s,%s,%s) RETURNING *;
        """
        params = (
            survey_id,
            body.id_question_type,
            body.text,
            created_at,
            updated_at,
            body.is_active
        )
        cursor.execute(query, params)
        new_question = cursor.fetchone()
        cursor.connection.commit()
        response = {
            "id": new_question['id'],
            "survey": survey_exists,
            "question_type": question_type_exists,
            "text": new_question['text'],
            "created_at": new_question['created_at'],
            "updated_at": new_question['updated_at'],
            "is_active": new_question['is_active']
        }
        return {"question": response}
    except RuntimeError as e:
        cursor.connection.rollback()
        raise e
    except Exception as e:
        cursor.connection.rollback()
        raise RuntimeError(f"Error creating survey question: {str(e)}")


def create_survey_question_option_controller(question_id: int, body: SurveyOptionSchema):
    try:
        question_check_query = "SELECT * FROM question WHERE id = %s;"
        cursor.execute(question_check_query, (question_id,))
        question_exists = cursor.fetchone()
        if not question_exists:
            raise RuntimeError(f"La pregunta con id {question_id} no existe.")
        # Only allowed for single_choice or multiple_choice questions.
        # You must enforce this rule at either the application or database level — explain your choice.
        id_question_type = question_exists['id_question_type']
        question_type_check_query = "SELECT * FROM question_type WHERE id = %s;"
        cursor.execute(question_type_check_query, (id_question_type,))
        question_type_exists = cursor.fetchone()
        print(question_type_exists)
        if not question_type_exists["allow_options"]:
            raise RuntimeError(
                f"El tipo de pregunta con id {id_question_type} no permite opciones.")

        query = """
        INSERT INTO option(question_id,text)
        VALUES (%s,%s) RETURNING *;
        """
        params = (question_id, body.text)
        cursor.execute(query, params)
        new_option = cursor.fetchone()
        cursor.connection.commit()
        response = {
            "id": new_option["id"],
            "question_id": new_option["question_id"],
            "text": new_option["text"]
        }
        return {"option": response}
    except RuntimeError as e:
        cursor.connection.rollback()
        raise e


def create_survey_question_type_controller(body: SurveyQuestionTypeSchema):
    try:
        query = """
        INSERT INTO question_type (title,description,allow_options)
        VALUES (%s,%s,%s) RETURNING *;
        """
        params = (body.title, body.description, body.allow_options)
        cursor.execute(query, params)
        response = cursor.fetchone()
        cursor.connection.commit()
        return {"question_type": response}
    except IntegrityError as ie:
        cursor.connection.rollback()
        if "unique_title" in str(ie) or "duplicate key" in str(ie):
            raise RuntimeError(f"El título '{body.title}' ya existe.")
        raise RuntimeError(f"Database integrity error: {str(ie)}")

    except Exception as e:
        cursor.connection.rollback()
        raise RuntimeError(f"Error creating survey question option: {str(e)}")


# endpoint para listar los tipos de preguntas
def get_survey_question_type_controller():
    print("question_types")
    try:
        query = """
        SELECT * FROM question_type;
        """
        cursor.execute(query)
        question_types = cursor.fetchall()
        return {"question_types": question_types}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_survey_by_id_controller(survey_id: int):
    try:
        query = """
        SELECT
            s.id AS survey_id,
            s.title AS survey_title,
            s.description AS survey_description,
            s.created_at AS survey_created_at,

            q.id AS question_id,
            q.text AS question_text,
            qt.id AS question_type_id,
            qt.title AS question_type_title,
            qt.description AS question_type_description,
            qt.allow_options AS question_type_allow_options,

            o.id AS option_id,
            o.text AS option_text

        FROM survey s
        JOIN question q ON q.survey_id = s.id
        JOIN question_type qt ON qt.id = q.id_question_type
        LEFT JOIN option o ON o.question_id = q.id
        WHERE s.id = %s AND s.is_active = TRUE
        ORDER BY q.id, o.id;
        """
        cursor.execute(query, (survey_id,))
        rows = cursor.fetchall()
        print(rows)
        if not rows:
            return None
        survey = {
            "id": rows[0]["survey_id"],
            "title": rows[0]["survey_title"],
            "description": rows[0]["survey_description"],
            "created_at": rows[0]["survey_created_at"],
            "questions": []
        }

        questions_dict = {}

        for row in rows:
            q_id = row["question_id"]
            if q_id not in questions_dict:
                question = {
                    "id": q_id,
                    "text": row["question_text"],
                    "question_type": {
                        "id": row["question_type_id"],
                        "title": row["question_type_title"],
                        "description": row["question_type_description"],
                        "allow_options": row["question_type_allow_options"],
                    },
                    "options": []
                }
                questions_dict[q_id] = question
                survey["questions"].append(question)

            if row["option_id"]:
                questions_dict[q_id]["options"].append({
                    "id": row["option_id"],
                    "text": row["option_text"]
                })

        return {"survey": survey}
    except Exception as e:
        print(f"Error retrieving survey by id {survey_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
