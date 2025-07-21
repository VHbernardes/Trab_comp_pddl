; problem_json_invalido.pddl
; Problema JSON com erro sintático: palavra-chave errada e parênteses faltando

(define
  (problem problem_json)
  (:domain domain_json)
  (:obects  ; erro de digitação aqui
    meu_objeto - objeto
    nome idade - chave
    "Victor" "25" - valor
  )
  (:init)
  (:goal (par_chave_valor meu_objeto nome "Victor"  ; falta fechar o parêntese aqui
)
