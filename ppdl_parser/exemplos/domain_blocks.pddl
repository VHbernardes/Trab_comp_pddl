; domain_blocks.pddl
; Um dominio PDDL para o problema de empilhar blocos

(define (domain blocks-world)
    (:requirements :strips :typing) ; Requisitos: strips (acoes instantaneas), typing (tipos)

    (:types
        block pile - object ; Define dois tipos: 'block' e 'pile', ambos subtipos de 'object'
    )

    (:predicates
        (on ?b1 - block ?b2 - block) ; ?b1 esta em cima de ?b2
        (ontable ?b - block) ; ?b esta na mesa
        (clear ?x - object) ; ?x (pode ser bloco ou pilha) nao tem nada em cima
        (handempty) ; A mao do robo esta vazia
        (holding ?b - block) ; O robo esta segurando ?b
    )

    (:action pick-up
        :parameters (?b - block) ; Acao para pegar um bloco da mesa
        :precondition (and (ontable ?b) (clear ?b) (handempty)) ; Condicoes para pegar: bloco na mesa, livre, mao vazia
        :effect (and (not (ontable ?b)) (not (clear ?b)) (not (handempty)) (holding ?b)) ; Efeitos: bloco nao esta mais na mesa/livre, mao nao vazia, robo segurando bloco
    )

    (:action put-down
        :parameters (?b - block) ; Acao para largar um bloco na mesa
        :precondition (holding ?b) ; Condicoes: robo segurando o bloco
        :effect (and (not (holding ?b)) (clear ?b) (handempty) (ontable ?b)) ; Efeitos: robo nao esta mais segurando, bloco livre, mao vazia, bloco na mesa
    )

    (:action stack
        :parameters (?b1 - block ?b2 - block) ; Acao para empilhar b1 em b2
        :precondition (and (holding ?b1) (clear ?b2)) ; Condicoes: robo segurando b1, b2 esta livre
        :effect (and (not (holding ?b1)) (not (clear ?b2)) (clear ?b1) (on ?b1 ?b2) (handempty)) ; Efeitos: robo nao segurando b1, b2 nao livre, b1 livre (agora esta em cima), b1 em b2, mao vazia
    )

    (:action unstack
        :parameters (?b1 - block ?b2 - block) ; Acao para desempilhar b1 de b2
        :precondition (and (on ?b1 ?b2) (clear ?b1) (handempty)) ; Condicoes: b1 em b2, b1 livre, mao vazia
        :effect (and (not (on ?b1 ?b2)) (not (clear ?b1)) (not (handempty)) (holding ?b1) (clear ?b2)) ; Efeitos: b1 nao mais em b2, b1 nao mais livre, mao nao vazia, robo segurando b1, b2 livre
    )
)