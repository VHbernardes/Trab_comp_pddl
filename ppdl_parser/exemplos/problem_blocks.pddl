; problem_blocks.pddl
; Um problema simples para o dominio blocks-world: A em cima de B, B na mesa

(define (problem blocks-a-on-b)
    (:domain blocks-world) ; Referencia ao dominio blocks-world

    (:objects
        a b - block ; Define dois objetos do tipo 'block': a e b
    )

    (:init
        (ontable b) ; B esta na mesa
        (clear b)   ; B esta livre
        (ontable a) ; A esta na mesa
        (clear a)   ; A esta livre
        (handempty) ; A mao do robo esta vazia
    )

    (:goal
        (and
            (on a b) ; O objetivo e que A esteja em cima de B
            (ontable b) ; E B esteja na mesa
        )
    )
)