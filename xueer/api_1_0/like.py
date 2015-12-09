# coding: utf-8

"""
    点赞API

"""
from . import api
from flask import g, jsonify, request
from xueer import db
from xueer.api_1_0.authentication import auth
from xueer.models import Courses, Comments


# 权限处理
@api.route('/courses/<int:id>/like/', methods=["GET", "PUT", "DELETE"])
@auth.login_required
def new_courses_id_like(id):
    """
    点赞特定id的课程
    :param id:
    :return:
    """
    course = Courses.query.get_or_404(id)
    if request.method == "PUT":
        if course.liked:
            return jsonify({
                'error': '你已经点赞过该课程'
            })
        else:
            course.users.append(g.current_user)
            db.session.add(course)
            db.session.commit()
            course.likes = len(course.users.all())
            db.session.add(course)
            db.session.commit()
            course = Courses.query.get_or_404(id)
            return jsonify(
                course.to_json()
            ), 201
    elif request.method == "DELETE":
        """
        删除特定id的评论
        :param id:
        :return:
        """
        if course.liked:
            course.users.remove(g.current_user)
            db.session.add(course)
            db.session.commit()
            course.likes = len(course.users.all())
            db.session.add(course)
            db.session.commit()
            course = Courses.query.get_or_404(id)
            return jsonify(
                course.to_json()
            ), 200
        else:
            return jsonify({
                "error": "你还没有点赞这门课程哦!"
            }), 403


@api.route('/comments/<int:id>/like/', methods=["GET", "PUT", "DELETE"])
@auth.login_required
def new_comments_id_like(id):
    """
    点赞特定id的课程
    :param id:
    :return:
    """
    comment = Comments.query.get_or_404(id)
    if request.method == "PUT":
        if comment.liked:
            return jsonify({
                'error': '你已经点赞过该评论'
            })
        else:
            comment.user.append(g.current_user)
            db.session.add(comment)
            db.session.commit()
            comment.likes = len(comment.user.all())
            db.session.add(comment)
            db.session.commit()
            comment = Comments.query.get_or_404(id)
            return jsonify(
                comment.to_json()
            ), 201
    elif request.method == "DELETE":
        """
        删除特定id的评论点赞
        :param id:
        :return:
        """
        if comment.liked:
            comment.user.remove(g.current_user)
            db.session.add(comment)
            db.session.commit()
            comment.likes = len(comment.user.all())
            db.session.add(comment)
            db.session.commit()
            comment = Comments.query.get_or_404(id)
            return jsonify(
                comment.to_json()
            ), 200
        else:
            return jsonify({
                "error": "你还没有点赞这个评论哦!"
            }), 403
