from pydantic import BaseModel


class CourseContentPublic(BaseModel):
    """Vue 'étudiant' d'un cours : contenu + vidéo.
    Nom volontairement différent de CoursePublic (admin) pour ne jamais
    entrer en conflit avec le schéma existant de ton dashboard admin.
    """
    id: str
    module_id: str
    level: str
    title: str
    content_html: str
    video_url: str
