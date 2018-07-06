"""routes.py: Each function in this file indicates a web page (HTML page)."""
from src.surfing_penguin.routes import api
from flask_restplus import Resource, fields
from src.surfing_penguin.db_interface import SurveyFunctions


# TODO: separate expected and returned api models
# TODO: add help and others (like default) for each field
api_return_message = api.model("return_message_model", {
        'messages': fields.String
    })

api_get_survey_name = api.model("survey_name", {
        'name': fields.String,
    })

api_get_survey_id = api.model("survey_id", {
        'id': fields.Integer
    })

api_question = api.model("question_model", {
        'idx': fields.Integer,
        'title': fields.String,
        'content': fields.String
    })

api_get_survey = api.model("get_survey_model", {
        'surveyname': fields.String,
        'questions': fields.List(fields.Nested(api_question))
    })

# TODO: add question_num and category (for meta class) in api_survey
api_return_survey = api.model("return_survey_model", {
        'id': fields.Integer,
        'question_num': fields.Integer,
        'surveyname': fields.String,
        'questions': fields.List(fields.Nested(api_question))
    })

api_answer = api.model("answer_model", {
        'idx': fields.Integer,
        'content': fields.String
    })

api_answerlist = api.model("answerlist_model", {
        'answers': fields.List(fields.Nested(api_answer)),
        'messages': fields.String
    })

api_get_answerlist = api.model("get_answerlist_model", {
        'survey_id': fields.Integer,
        'answers': fields.List(fields.Nested(api_answer))
    })

api_return_answerlists = api.model("return_ansewrlists_model", {
        'survey_id': fields.Integer,
        'answerlist_num': fields.Integer,
        'answerlists': fields.List(fields.Nested(api_answerlist))
    })


""" survey associated APIs """
# TODO: add error handling for functions that change the database
# (e.g., creating a survey with existing name)


@api.route(f'/create_survey')
class create_survey(Resource):
    @api.marshal_with(api_return_message)
    @api.expect(api_get_survey)
    def post(self):
        SurveyFunctions.new_survey(
                api.payload['surveyname'], api.payload['questions'])
        return {'messages': "Survey created"}


@api.route(f'/show_all_surveys')
class show_surveys(Resource):
    @api.marshal_list_with(api_return_survey)
    def get(self):
        return SurveyFunctions.get_all_surveys()


@api.route(f'/search_survey_by_id')
class search_survey_by_id(Resource):
    """
    Show the information of a survey, given its name or ID.
    """
    @api.marshal_list_with(api_return_survey)
    @api.expect(api_get_survey_id)
    def post(self):
        return SurveyFunctions.id_get_survey(api.payload['id'])


@api.route(f'/search_survey_by_name')
class search_survey_by_name(Resource):
    """
    Show the information of a survey, given its name or ID.
    """
    @api.marshal_list_with(api_return_survey)
    @api.expect(api_get_survey_name)
    def post(self):
        return SurveyFunctions.name_get_survey(api.payload['name'])


@api.route(f'/answer_a_survey')
class answer_survey(Resource):
    @api.marshal_with(api_return_message)
    @api.expect(api_get_answerlist)
    def post(self):
        if SurveyFunctions.id_get_survey(api.payload['survey_id']):
            SurveyFunctions.new_answerlist(api.payload)
            return {'messages': "Answer completed"}
        return {'messages': "Survey not found"}


@api.route(f'/show_answers')
class show_answerlists(Resource):
    @api.marshal_with(api_return_answerlists)
    @api.expect(api_get_survey_id)
    def post(self):
        if SurveyFunctions.id_get_survey(api.payload['id']):
            return {
                "survey_id": api.payload['id'],
                "answerlist_num":
                    SurveyFunctions.id_get_answerlist_num(api.payload['id']),
                "answerlists":
                    SurveyFunctions.id_get_answerlists(api.payload['id'])
            }
        return {'messages': "Survey not found"}
