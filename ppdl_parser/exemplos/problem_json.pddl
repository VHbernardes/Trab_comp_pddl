; problem_json.pddl
; Problema para testar adição e remoção de pares chave-valor em objeto JSON.

(define
  (problem problem_json)
  (:domain domain_json)
  (:objects
    meu_objeto - objeto
    nome idade - chave
    Victor vinteecinco - valor
  )
  (:init)
  (:goal (par_chave_valor meu_objeto nome Victor))
)
