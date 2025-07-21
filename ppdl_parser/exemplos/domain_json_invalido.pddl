; domain_json_invalido.pddl
; Domínio JSON com erro sintático: parênteses desbalanceados e nome da ação errado

(define
  (domain domain_json)
  (:requirements :strips)
  (:predicates
    (par_chave_valor ?obj - objeto ?chave - chave ?valor - valor) ; <- falta fechar aqui!
  (:action say_hallo  ; erro no nome da ação
    :parameters (?obj - objeto ?chave - chave ?valor - valor)
    :precondition ()
    :effect (par_chave_valor ?obj ?chave ?valor)
  )
)
