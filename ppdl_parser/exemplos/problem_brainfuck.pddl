; problem_brainfuck.pddl
; Problema para testar incremento e controle de loop.
; A célula inicia em 0, objetivo é chegar em 3 com loop ativo.

(define
  (problem loop_incremento)
  (:domain brainfuck_simples)
  (:init (= (celula) 0))
  (:goal (and
    (loop_ativo)
    (= (celula) 3)
  ))
)
