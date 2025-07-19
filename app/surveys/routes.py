from fastapi import APIRouter

from app.surveys.controller import create_survey_controller, create_survey_question_controller, create_survey_question_option_controller, create_survey_question_type_controller, get_survey_by_id_controller, get_survey_question_type_controller
from app.surveys.schema import SurveyCreateSchema, SurveyOptionSchema, SurveyQuestionSchema, SurveyQuestionTypeSchema


router = APIRouter(
    prefix="/surveys",
    tags=["Surveys"],
)


@router.get("/")
def welcome_project():
    return {"message": "welcome to the survey project"}


@router.get("/question_type")
def get_survey_question_type():
    try:
        return get_survey_question_type_controller()
    except RuntimeError as e:
        return {"error": str(e)}


@router.get("/{survey_id}")
def get_survey_by_id(survey_id: int):
    try:
        return get_survey_by_id_controller(survey_id)
    except Exception as e:
        return {"error": str(e)}


@router.post("")
def create_survey(body: SurveyCreateSchema):
    try:
        return create_survey_controller(body)
    except RuntimeError as e:
        return {"error": str(e)}


@router.post("/{survey_id}/questions")
def create_survey_question(survey_id: int, body: SurveyQuestionSchema):
    try:
        return create_survey_question_controller(survey_id, body)
    except RuntimeError as e:
        return {"error": str(e)}


@router.post("/questions/question_type")
def create_survey_question_type(body: SurveyQuestionTypeSchema):
    try:
        return create_survey_question_type_controller(body)
    except RuntimeError as e:
        return {"error": str(e)}


@router.post("/questions/{question_id}/options")
def create_survey_question_option(question_id: int, body: SurveyOptionSchema):
    try:
        return create_survey_question_option_controller(question_id, body)
    except RuntimeError as e:
        return {"error": str(e)}
