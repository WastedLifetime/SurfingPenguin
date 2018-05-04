"""routes.py: Each function in this file indicates a web page (HTML page)."""
from src.surfing_penguin import __version__
from src.surfing_penguin import api
from flask_restplus import Resource, fields
from src.surfing_penguin.db_interface import SurveyFunctions

__version__ = __version__[0:3]

# TODO: separate expected and returned api models
# TODO: add help and others (like default) for each field
api_return_message = api.model("return_message_model", {
        'messages': fields.String
    })

api_survey_name = api.model("survey_name", {
        'name': fields.String,
    })

api_survey_id = api.model("survey_id", {
        'id': fields.Integer
    })

api_question = api.model("question_model", {
        'idx': fields.Integer,
        'title': fields.String,
        'content': fields.String
    })

# TODO: add question_num and category (for meta class) in api_survey
api_survey = api.model("survey_model", {
        'id': fields.Integer,
        'surveyname': fields.String,
        'questions': fields.List(fields.Nested(api_question))
    })

""" survey associated APIs """
# TODO: add error handling for functions that change the database
# (e.g., creating a survey with existing name)


@api.route(f'/api/{__version__}/create_survey')
class create_survey(Resource):
    @api.marshal_with(api_return_message)
    @api.expect(api_survey)
    def post(self):
        SurveyFunctions.new_survey(
                api.payload['surveyname'], api.payload['questions'])
        return {'messages': "Survey created"}


@api.route(f'/api/{__version__}/show_all_surveys')
class show_surveys(Resource):
    @api.marshal_list_with(api_survey)
    def get(self):
        return SurveyFunctions.get_all_surveys()


@api.route(f'/api/{__version__}/search_survey_by_id')
class search_survey_by_id(Resource):
    """
    Show the information of a survey, given its name or ID.
    """
    @api.marshal_list_with(api_survey)
    @api.expect(api_survey_id)
    def post(self):
        return SurveyFunctions.id_get_survey(api.payload['id'])


@api.route(f'/api/{__version__}/search_survey_by_name')
class search_survey_by_name(Resource):
    """
    Show the information of a survey, given its name or ID.
    """
    @api.marshal_list_with(api_survey)
    @api.expect(api_survey_name)
    def post(self):
        return SurveyFunctions.name_get_survey(api.payload['name'])
