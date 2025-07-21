; domain_lights.pddl
; Domínio simples para ligar e desligar luzes em diferentes cômodos.
; Usa tipos e uma função para controlar intensidade da luz.

(define
  (domain luzes)
  (:requirements :strips :typing :fluents)
  (:types comodo)
  (:predicates
    (luz_ligada ?c - comodo)
  )
  (:functions
    (intensidade ?c - comodo)
  )
  (:action ligar_luz
    :parameters (?c - comodo)
    :precondition (not (luz_ligada ?c))
    :effect (and
      (luz_ligada ?c)
      (assign (intensidade ?c) 100)
    )
  )
  (:action desligar_luz
    :parameters (?c - comodo)
    :precondition (luz_ligada ?c)
    :effect (and
      (not (luz_ligada ?c))
      (assign (intensidade ?c) 0)
    )
  )
)
