# from flask import jsonify
# # from flask_mail import Mail, Message
# # mail = Mail()

# def sendMail(subject, name, from_email, to_email):
#     msg = Message(subject, sender = (name, from_email) , recipients= [to_email])
#     msg.html = '<h1>Usuario Creado</h1>'
#     mail.send(msg)
#     return jsonify({"msg": "Email sent succefully"}), 200


# def allowed_file(filename, ALLOWED_EXTENSION):
#     return '.' in filename and \
#             filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION