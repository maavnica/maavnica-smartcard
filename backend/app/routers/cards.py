from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


# -------------------------------------------------------------------
# CRÉATION D'UNE CARTE (ADMIN)
# -------------------------------------------------------------------
@router.post("/", status_code=201)
def create_card(card_in: schemas.CardCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle SmartCard.
    Utilisée par l'admin quand currentCardId est vide.
    """
    # vérifier unicité du slug
    existing = db.query(models.Card).filter(models.Card.slug == card_in.slug).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Ce slug est déjà utilisé par une autre carte.",
        )

    card = models.Card(**card_in.dict())
    db.add(card)
    db.commit()
    db.refresh(card)
    return card  # renvoyé tel quel au front (JSON)


# -------------------------------------------------------------------
# MISE À JOUR D'UNE CARTE (ADMIN)
# -------------------------------------------------------------------
@router.put("/{card_id}")
def update_card(card_id: int, card_in: schemas.CardUpdate, db: Session = Depends(get_db)):
    """
    Met à jour une SmartCard existante.
    Utilisée par l'admin quand currentCardId est défini.
    """
    card = db.query(models.Card).get(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    data = card_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(card, field, value)

    db.commit()
    db.refresh(card)
    return card


# -------------------------------------------------------------------
# RÉCUPÉRER UNE CARTE PAR SON SLUG (ADMIN)
# -------------------------------------------------------------------
@router.get("/by-slug/{slug}")
def get_card_by_slug(slug: str, db: Session = Depends(get_db)):
    """
    Récupère une carte par son slug.
    Utilisée dans l'admin avec le bouton "Charger ma carte".
    """
    card = db.query(models.Card).filter(models.Card.slug == slug).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


# -------------------------------------------------------------------
# LISTE DES AVIS (ADMIN)
# -------------------------------------------------------------------
@router.get("/{card_id}/feedback")
def list_feedback(card_id: int, db: Session = Depends(get_db)) -> List[schemas.FeedbackOut]:
    """
    Liste tous les avis rapides liés à une carte.
    Affiché dans la colonne droite de l'admin.
    """
    card = db.query(models.Card).get(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    feedbacks = (
        db.query(models.Feedback)
        .filter(models.Feedback.card_id == card_id)
        .order_by(models.Feedback.created_at.desc())
        .all()
    )
    return feedbacks


# -------------------------------------------------------------------
# LISTE DES DEMANDES DE DEVIS (ADMIN)
# -------------------------------------------------------------------
@router.get("/{card_id}/quotes")
def list_quotes(card_id: int, db: Session = Depends(get_db)) -> List[schemas.QuoteOut]:
    """
    Liste toutes les demandes de devis liées à une carte.
    Affiché dans la colonne droite de l'admin.
    """
    card = db.query(models.Card).get(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    quotes = (
        db.query(models.Quote)
        .filter(models.Quote.card_id == card_id)
        .order_by(models.Quote.created_at.desc())
        .all()
    )
    return quotes


