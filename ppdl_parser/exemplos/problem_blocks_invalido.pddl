; problem_blocks_invalido.pddl
; Problema blocks com erro: objetos sem tipo definido e define não fechado

(define
  (problem problem_blocks)
  (:domain domain_blocks)
  (:objects
    block1 block2 block3  ; faltou definir o tipo '- block'
    arm
  )
  (:init
    (clear block1)
    (ontable block2)
  )
  (:goal (and (on block1 block2) (on block2 block3)))
