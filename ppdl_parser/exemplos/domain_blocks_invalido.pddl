; domain_blocks_invalido.pddl
; Domínio blocks com erro: ausência de :action e parênteses mal fechados

(define
  (domain domain_blocks)
  (:requirements :strips)
  (:predicates
    (on ?x - block ?y - block)
    (clear ?x - block)
    (ontable ?x - block)
    (handempty)
    (holding ?x - block)
  ) ; fecha predicates
  ; falta a palavra-chave :action, só tem o nome e parâmetros errado
  move_block
    :parameters (?x - block ?y - block)
    :precondition (and (clear ?y) (holding ?x))
    :effect (and (not (holding ?x)) (on ?x ?y))
)
