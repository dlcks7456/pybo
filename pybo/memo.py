kw = request.args.get('kw', type=str, default='')  # 검색어

# 검색
search = '%%{}%%'.format(kw)
sub_query = db.session.query(Answer.question_id, Answer.content, User.username)
    .join(User, Answer.user_id == User.id).subquery()
question_list = Question.query
    .join(User)
    .outerjoin(sub_query, sub_query.c.question_id == Question.id)
    .filter(Question.subject.ilike(search) |      # 질문제목
            Question.content.ilike(search) |      # 질문내용
            User.username.ilike(search) |         # 질문작성자
            sub_query.c.content.ilike(search) |   # 답변내용
            sub_query.c.username.ilike(search)    # 답변작성자
            )
    .distinct()