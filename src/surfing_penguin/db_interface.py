from surfing_penguin import api, session
from surfing_penguin.models import User


class UserFunctions(object):
    def search_user(name):
        if session.query(User).filter_by(username=name).first() is not None:
            return True
        return False

    def get_user(name):
        return session.query(User).filter_by(username=name).first()

    def register(name, password):
        if session.query(User).filter_by(username=name).first() is not None:
            return
        new_user = User(name, password)
        new_user.id = session.query(User).count() + 1
        session.add(new_user)
        session.commit()
        return new_user

    def check_password(name, password):
        user = session.query(User).filter_by(username=name).first()
        return user.verify_password(password)

    def get_all_users():
        users = session.query(User).all()
        return users

    def delete_user(name):
        session.query(User).filter_by(username=name).delete()
        session.commit()


class Qstnr(object):
    def __init__(self):
        self.iter = 0
        self.questions = []

    def get(self, id):
        for qst in self.questions:
            if qst['id'] == id:
                return qst
        api.abort(404, "question {} doesn't exist".format(id))

    def new_qst(self, data):
        question = data
        self.iter = self.iter + 1
        question['id'] = self.iter
        self.questions.append(question)
        return question

    def delete(self, id):
        question = self.get(id)
        self.question.remove(question)
