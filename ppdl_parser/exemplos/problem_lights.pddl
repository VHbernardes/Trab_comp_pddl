; problem_lights.pddl
; Problema simples para o domínio das luzes.
; Dois cômodos, luz desligada inicialmente, objetivo ligar a luz do quarto.

(define
  (problem acender_luz_quarto)
  (:domain luzes)
  (:objects quarto sala - comodo)
  (:init
    (not (luz_ligada quarto))
    (not (luz_ligada sala))
    (= (intensidade quarto) 0)
    (= (intensidade sala) 0)
  )
  (:goal (luz_ligada quarto))
)
