def serialize_query_result(ClassName):
    return map(ClassName.to_dict, ClassName.query.all())