; problem_helloworld.pddl
; Um problema PDDL muito simples para o dominio helloworld-domain

(define (problem helloworld-problem)
    (:domain helloworld-domain)
    (:objects) ; Nao ha objetos neste problema
    (:init
        (not (hello-pddl)) ; Inicialmente, hello-pddl e falso
    )
    (:goal
        (hello-pddl) ; O objetivo e que hello-pddl se torne verdadeiro
    )
)