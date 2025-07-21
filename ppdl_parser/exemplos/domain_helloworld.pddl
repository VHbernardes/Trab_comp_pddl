; domain_helloworld.pddl
; Um dominio PDDL muito simples

(define
  (domain ola_mundo)
  (:requirements :strips)
  (:predicates (disse_ola))
  (:action diga_ola
    :precondition ()
    :effect (disse_ola)
  )
)