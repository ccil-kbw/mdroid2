from django.shortcuts import render

# Create your views here.
class Client:
    def __init__(self):
        self.url = os.environ.get("MDROID2_DATABASE_URL")
        if self.url is None:
            raise ValueError("MDROID2_DATABASE_URL environment variable is required.")

    def __session(self):
        return sessionmaker(bind=create_engine(self.url))()

    def get_iqama_sources(self) -> List[Type[IqamaSource]]:
        return self.__session().query(IqamaSource).all()
