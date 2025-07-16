from pydantic import BaseModel
from typing import Optional

class SurveyCreateSchema(BaseModel):
  title: str
  description: Optional[str] = None
  is_active: Optional[bool] = True

class SurveyQuestionTypeSchema(BaseModel):
  title: str
  description: Optional[str] = None
  allow_options: Optional[bool] = True

class SurveyQuestionSchema(BaseModel):
  id_question_type:int
  text: str
  is_active: Optional[bool] = True

class SurveyOptionSchema(BaseModel):
  text:str
  
