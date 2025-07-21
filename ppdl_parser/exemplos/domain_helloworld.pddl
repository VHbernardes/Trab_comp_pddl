; domain_helloworld.pddl
; Um dominio PDDL muito simples

(define (domain helloworld-domain)
    (:requirements :strips)
    (:predicates
        (hello-pddl) ; Um predicado simples que pode ser verdadeiro ou falso
    )
)