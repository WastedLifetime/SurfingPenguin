from flask_restplus import Resource, fields
from src.surfing_penguin.routes import api
from src.surfing_penguin.db_interface import survey_functions


api_return_message = api.model("return_message_model", {
        'messages': fields.String(description="Messages returned")
    })

api_get_survey_name = api.model("survey_name", {
        'name': fields.String(description="Survey name"),
    })

api_get_survey_id = api.model("survey_id", {
        'id': fields.Integer(description="Survey ID")
    })

api_question = api.model("question_model", {
        'idx': fields.Integer(description="Index in that survey"),
        'title': fields.String(description="Question"),
        'content': fields.String(description="Description of the question")
    })

api_get_survey = api.model("get_survey_model", {
        'surveyname': fields.String(description="Survey name"),
        'questions': fields.List(
            fields.Nested(api_question),
            description="All questions in the survey"
            )
    })

# TODO: add question_num and category (for meta class) in api_survey
api_return_survey = api.model("return_survey_model", {
        'id': fields.Integer(description="Survey ID"),
        'question_num': fields.Integer(
            description="Number of questions in the survey"),
        'surveyname': fields.String(description="Survey name"),
        'questions': fields.List(
            fields.Nested(api_question),
            description="All questions in the survey"
            )
    })

api_answer = api.model("answer_model", {
        'idx': fields.Integer(description="Question index in that survey"),
        'content': fields.String(description="Answer content")
    })

api_answerlist = api.model("answerlist_model", {
        'answers': fields.List(
            fields.Nested(api_answer),
            description="All answers of the survey"),
        'messages': fields.String(description="Messages returned")
    })

api_get_answerlist = api.model("get_answerlist_model", {
        'survey_id': fields.Integer(description="Survey ID"),
        'answers': fields.List(
            fields.Nested(api_answer),
            description="All answers of the survey"),
    })

api_return_answerlists = api.model("return_ansewrlists_model", {
        'survey_id': fields.Integer(description="Survey ID"),
        'answerlist_num': fields.Integer(description="Number of answerlists"),
        'answerlists': fields.List(
            fields.Nested(api_answerlist),
            description="All answerlists of the survey"),
        'messages': fields.String(description="Messages returned")
    })


""" survey associated APIs """


@api.route('/create_survey')
class create_survey(Resource):
    @api.marshal_with(api_return_message)
    @api.expect(api_get_survey)
    def post(self):
        try:
            if api.payload['surveyname'] is None:
                return {'messages': "Invalid input: No survey name"}, 400
            # TODO: Check if an user duplicates his/her survey
            survey_functions.new_survey(
                    api.payload['surveyname'], api.payload['questions'])
            return {'messages': "Survey created"}
        except KeyError:
            return {'messages': "Invalid input format"}, 400


@api.route('/show_all_surveys')
class show_surveys(Resource):
    @api.marshal_list_with(api_return_survey)
    def get(self):
        return survey_functions.get_all_surveys()


@api.route('/search_survey_by_id')
class search_survey_by_id(Resource):
    """
    Show the information of a survey, given its name or ID.
    """
    @api.marshal_list_with(api_return_survey)
    @api.expect(api_get_survey_id)
    def post(self):
        return survey_functions.id_get_survey(api.payload['id'])


@api.route('/search_survey_by_name')
class search_survey_by_name(Resource):
    """
    Show the information of a survey, given its name or ID.
    """
    @api.marshal_list_with(api_return_survey)
    @api.expect(api_get_survey_name)
    def post(self):
        return survey_functions.name_get_survey(api.payload['name'])


@api.route('/answer_a_survey')
class answer_survey(Resource):
    @api.marshal_with(api_return_message)
    @api.expect(api_get_answerlist)
    def post(self):
        try:
            if survey_functions.id_get_survey(api.payload['survey_id']):
                survey_functions.new_answerlist(api.payload)
                return {'messages': "Answer completed"}
            return {'messages': "Survey not found"}, 400
        except KeyError:
            return {'messages': "Invalid input format"}, 400


@api.route('/show_answers')
class show_answerlists(Resource):
    ''' Show all answerlists of a survey '''
    @api.marshal_with(api_return_answerlists)
    @api.expect(api_get_survey_id)
    def post(self):
        try:
            if survey_functions.id_get_survey(api.payload['id']):
                return {
                    "survey_id": api.payload['id'],
                    "answerlist_num":
                        survey_functions.id_get_answerlist_num(
                            api.payload['id']),
                    "answerlists":
                        survey_functions.id_get_answerlists(api.payload['id'])
                }
            return {'messages': "Survey not found"}, 400
        except KeyError:
            return {'messages': "Invalid input format"}, 400