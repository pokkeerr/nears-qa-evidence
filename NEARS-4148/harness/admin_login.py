import sys; sys.path.insert(0,'.')
from q import *
from forms import FormHarvest
def admin_jar(srv='fixed'):
    j=Jar(srv,'admin'); r=j.req('GET','/login/admin'); j.token=tok(r.text); cap=j.captcha()
    r=j.req('POST','/login_submit',data={'email':'admin@admin.com','password':'123456789','role':'admin','custome_recaptcha':cap})
    return j,r
if __name__=='__main__':
    j,r=admin_jar(); print(summarize(r))
    r=j.req('GET','/admin/business-settings/business-setup/business'); print(r.status_code, len(r.text))
    j.token=tok(r.text)
    h=FormHarvest('update-setup'); h.feed(r.text); print(len(h.fields)); print([f for f in h.fields if 'business_model' in f[0]])
