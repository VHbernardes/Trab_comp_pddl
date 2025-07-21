; domain_brainfuck.pddl
; Domínio que simula comandos Brainfuck para manipular uma célula de memória.
; Usa funções para valor da célula e controle de loop (simplificado).

(define
  (domain brainfuck_simples)
  (:requirements :strips :fluents)
  (:predicates
    (loop_ativo)
  )
  (:functions
    (celula)
  )
  (:action incrementar_celula
    :precondition ()
    :effect (assign (celula) (+ (celula) 1))
  )
  (:action decrementar_celula
    :precondition (> (celula) 0)
    :effect (assign (celula) (- (celula) 1))
  )
  (:action iniciar_loop
    :precondition (not (loop_ativo))
    :effect (loop_ativo)
  )
  (:action finalizar_loop
    :precondition (loop_ativo)
    :effect (not (loop_ativo))
  )
)
