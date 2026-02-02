from config import *

resend.api_key = os.getenv("RESEND_API_KEY")

r = resend.Emails.send({
 "from": "onboarding@resend.dev",
 "to": "miguel.ossa.abellan@gmail.com",
 "subject": "Hello World",
 "html": "<p>Congrats on sending your <strong>first email</strong>!</p>"
})