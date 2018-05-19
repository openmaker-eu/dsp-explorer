
class User:
    @classmethod
    def authorization(self, request):
        authorization = \
            1000 if request.user.is_superuser else \
            100 if False else \
            20 if False else \
            10 if request.user.is_authenticated \
            else 0
        return authorization