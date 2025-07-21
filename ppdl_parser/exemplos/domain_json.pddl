; domain_json.pddl
; Domínio simples para manipular pares chave-valor em um objeto JSON.
; Permite adicionar e remover pares.

(define
  (domain domain_json)
  (:requirements :strips :typing)
  (:types objeto chave valor)
  (:predicates
    (par_chave_valor ?o - objeto ?k - chave ?v - valor)
  )
  (:action adicionar_par
    :parameters (?o - objeto ?k - chave ?v - valor)
    :precondition (not (par_chave_valor ?o ?k ?v))
    :effect (par_chave_valor ?o ?k ?v)
  )
  (:action remover_par
    :parameters (?o - objeto ?k - chave ?v - valor)
    :precondition (par_chave_valor ?o ?k ?v)
    :effect (not (par_chave_valor ?o ?k ?v))
  )
)
