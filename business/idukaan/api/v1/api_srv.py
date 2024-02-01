from business import models as BMdl

def ValidateOrgEmpObj(user, org):
        try:
            return BMdl.OrgEmp.objects.get(user=user, org=org)
        except BMdl.OrgEmp.DoesNotExist:
            return None
        
def ValidateOrgObj(org):
    return org.is_active and org.is_kyo
