# uncompyle6 version 3.9.1
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Aug 23 2022, 17:18:36) 
# [GCC 11.2.0]
# Embedded file name: urlparse.py
"""Parse (absolute and relative) URLs.

urlparse module is based upon the following RFC specifications.

RFC 3986 (STD66): "Uniform Resource Identifiers" by T. Berners-Lee, R. Fielding
and L.  Masinter, January 2005.

RFC 2732 : "Format for Literal IPv6 Addresses in URL's by R.Hinden, B.Carpenter
and L.Masinter, December 1999.

RFC 2396:  "Uniform Resource Identifiers (URI)": Generic Syntax by T.
Berners-Lee, R. Fielding, and L. Masinter, August 1998.

RFC 2368: "The mailto URL scheme", by P.Hoffman , L Masinter, J. Zwinski, July 1998.

RFC 1808: "Relative Uniform Resource Locators", by R. Fielding, UC Irvine, June
1995.

RFC 1738: "Uniform Resource Locators (URL)" by T. Berners-Lee, L. Masinter, M.
McCahill, December 1994

RFC 3986 is considered the current standard and any future changes to
urlparse module should conform with it.  The urlparse module is
currently not entirely compliant with this RFC due to defacto
scenarios for parsing, and for backward compatibility purposes, some
parsing quirks from older RFCs are retained. The testcases in
test_urlparse.py provides a good indicator of parsing behavior.

"""
-- Stacks of completed symbols:
START ::= |- stmts . 
_come_froms ::= \e__come_froms . COME_FROM
_ifstmts_jump ::= \e_c_stmts_opt . JUMP_FORWARD come_froms
_ifstmts_jump ::= c_stmts_opt . JUMP_FORWARD come_froms
_ifstmts_jump ::= c_stmts_opt JUMP_FORWARD . come_froms
_ifstmts_jump ::= c_stmts_opt JUMP_FORWARD come_froms . 
_stmts ::= _stmts . stmt
_stmts ::= _stmts stmt . 
_stmts ::= stmt . 
and ::= expr . JUMP_IF_FALSE_OR_POP expr COME_FROM
and ::= expr . jmp_false expr \e_come_from_opt
and ::= expr . jmp_false expr come_from_opt
and ::= expr jmp_false . expr \e_come_from_opt
and ::= expr jmp_false . expr come_from_opt
and ::= expr jmp_false expr . come_from_opt
and ::= expr jmp_false expr \e_come_from_opt . 
and ::= expr jmp_false expr come_from_opt . 
assert ::= assert_expr . jmp_true LOAD_ASSERT RAISE_VARARGS_1
assert2 ::= assert_expr . jmp_true LOAD_ASSERT expr CALL_FUNCTION_1 RAISE_VARARGS_1
assert_expr ::= assert_expr_and . 
assert_expr ::= expr . 
assert_expr_and ::= assert_expr . jmp_false expr
assert_expr_and ::= assert_expr jmp_false . expr
assert_expr_and ::= assert_expr jmp_false expr . 
assert_expr_or ::= assert_expr . jmp_true expr
assign ::= expr . DUP_TOP designList
assign ::= expr . store
assign ::= expr store . 
assign2 ::= expr . expr ROT_TWO store store
assign2 ::= expr expr . ROT_TWO store store
assign3 ::= expr . expr expr ROT_THREE ROT_TWO store store store
assign3 ::= expr expr . expr ROT_THREE ROT_TWO store store store
assign3 ::= expr expr expr . ROT_THREE ROT_TWO store store store
attribute ::= expr . GET_ITER
attribute ::= expr . LOAD_ATTR
attribute ::= expr GET_ITER . 
attribute ::= expr LOAD_ATTR . 
aug_assign1 ::= expr . expr inplace_op ROT_FOUR STORE_SLICE+3
aug_assign1 ::= expr . expr inplace_op ROT_THREE STORE_SLICE+1
aug_assign1 ::= expr . expr inplace_op ROT_THREE STORE_SLICE+2
aug_assign1 ::= expr . expr inplace_op ROT_THREE STORE_SUBSCR
aug_assign1 ::= expr . expr inplace_op ROT_TWO STORE_SLICE+0
aug_assign1 ::= expr . expr inplace_op store
aug_assign1 ::= expr expr . inplace_op ROT_FOUR STORE_SLICE+3
aug_assign1 ::= expr expr . inplace_op ROT_THREE STORE_SLICE+1
aug_assign1 ::= expr expr . inplace_op ROT_THREE STORE_SLICE+2
aug_assign1 ::= expr expr . inplace_op ROT_THREE STORE_SUBSCR
aug_assign1 ::= expr expr . inplace_op ROT_TWO STORE_SLICE+0
aug_assign1 ::= expr expr . inplace_op store
aug_assign2 ::= expr . DUP_TOP LOAD_ATTR expr inplace_op ROT_TWO STORE_ATTR
bin_op ::= expr . expr binary_operator
bin_op ::= expr expr . binary_operator
bin_op ::= expr expr binary_operator . 
binary_operator ::= BINARY_MODULO . 
c_stmts ::= _stmts . 
c_stmts ::= _stmts . lastc_stmt
c_stmts ::= _stmts lastc_stmt . 
c_stmts ::= continues . 
c_stmts_opt ::= c_stmts . 
call ::= expr . CALL_FUNCTION_0
call ::= expr . expr CALL_FUNCTION_1
call ::= expr . expr expr CALL_FUNCTION_2
call ::= expr . expr expr expr CALL_FUNCTION_3
call ::= expr . expr expr expr expr expr CALL_FUNCTION_5
call ::= expr . expr expr expr expr expr expr CALL_FUNCTION_6
call ::= expr expr . CALL_FUNCTION_1
call ::= expr expr . expr CALL_FUNCTION_2
call ::= expr expr . expr expr CALL_FUNCTION_3
call ::= expr expr . expr expr expr expr CALL_FUNCTION_5
call ::= expr expr . expr expr expr expr expr CALL_FUNCTION_6
call ::= expr expr CALL_FUNCTION_1 . 
call ::= expr expr expr . CALL_FUNCTION_2
call ::= expr expr expr . expr CALL_FUNCTION_3
call ::= expr expr expr . expr expr expr CALL_FUNCTION_5
call ::= expr expr expr . expr expr expr expr CALL_FUNCTION_6
call ::= expr expr expr CALL_FUNCTION_2 . 
call_stmt ::= expr . POP_TOP
call_stmt ::= expr POP_TOP . 
classdefdeco1 ::= expr . classdefdeco1 CALL_FUNCTION_1
classdefdeco1 ::= expr . classdefdeco2 CALL_FUNCTION_1
classdefdeco2 ::= LOAD_CONST . expr mkfunc CALL_FUNCTION_0 BUILD_CLASS
classdefdeco2 ::= LOAD_CONST expr . mkfunc CALL_FUNCTION_0 BUILD_CLASS
come_from_opt ::= COME_FROM . 
come_froms ::= COME_FROM . 
come_froms ::= come_froms . COME_FROM
compare ::= compare_single . 
compare_chained ::= expr . compared_chained_middle ROT_TWO POP_TOP \e__come_froms
compare_chained ::= expr . compared_chained_middle ROT_TWO POP_TOP _come_froms
compare_single ::= expr . expr COMPARE_OP
compare_single ::= expr expr . COMPARE_OP
compare_single ::= expr expr COMPARE_OP . 
compared_chained_middle ::= expr . DUP_TOP ROT_THREE COMPARE_OP JUMP_IF_FALSE_OR_POP compare_chained_right COME_FROM
compared_chained_middle ::= expr . DUP_TOP ROT_THREE COMPARE_OP JUMP_IF_FALSE_OR_POP compared_chained_middle COME_FROM
continue ::= CONTINUE . 
continues ::= _stmts . lastl_stmt continue
continues ::= _stmts lastl_stmt . continue
continues ::= _stmts lastl_stmt continue . 
continues ::= continue . 
continues ::= lastl_stmt . continue
del_expr ::= expr . 
delete ::= del_expr . DELETE_SLICE+0
delete ::= del_expr . del_expr DELETE_SLICE+1
delete ::= del_expr . del_expr DELETE_SLICE+2
delete ::= del_expr . del_expr del_expr DELETE_SLICE+3
delete ::= del_expr del_expr . DELETE_SLICE+1
delete ::= del_expr del_expr . DELETE_SLICE+2
delete ::= del_expr del_expr . del_expr DELETE_SLICE+3
delete ::= del_expr del_expr del_expr . DELETE_SLICE+3
delete ::= expr . DELETE_ATTR
delete_subscript ::= expr . expr DELETE_SUBSCR
delete_subscript ::= expr expr . DELETE_SUBSCR
else_suitec ::= c_stmts . 
expr ::= LOAD_CONST . 
expr ::= LOAD_FAST . 
expr ::= LOAD_GLOBAL . 
expr ::= and . 
expr ::= attribute . 
expr ::= bin_op . 
expr ::= call . 
expr ::= compare . 
expr ::= get_iter . 
expr ::= list . 
expr ::= list_comp . 
expr ::= tuple . 
expr ::= unary_not . 
expr_jitop ::= expr . JUMP_IF_TRUE_OR_POP
expr_jt ::= expr . jmp_true
for ::= SETUP_LOOP . expr for_iter store for_block POP_BLOCK \e__come_froms
for ::= SETUP_LOOP . expr for_iter store for_block POP_BLOCK _come_froms
for ::= SETUP_LOOP expr . for_iter store for_block POP_BLOCK \e__come_froms
for ::= SETUP_LOOP expr . for_iter store for_block POP_BLOCK _come_froms
for ::= SETUP_LOOP expr for_iter . store for_block POP_BLOCK \e__come_froms
for ::= SETUP_LOOP expr for_iter . store for_block POP_BLOCK _come_froms
for ::= SETUP_LOOP expr for_iter store . for_block POP_BLOCK \e__come_froms
for ::= SETUP_LOOP expr for_iter store . for_block POP_BLOCK _come_froms
for_block ::= \e_l_stmts_opt . JUMP_ABSOLUTE JUMP_BACK JUMP_BACK
for_block ::= \e_l_stmts_opt . JUMP_BACK
for_block ::= \e_l_stmts_opt . _come_froms JUMP_BACK
for_block ::= \e_l_stmts_opt \e__come_froms . JUMP_BACK
for_block ::= l_stmts_opt . JUMP_ABSOLUTE JUMP_BACK JUMP_BACK
for_block ::= l_stmts_opt . JUMP_BACK
for_block ::= l_stmts_opt . _come_froms JUMP_BACK
for_block ::= l_stmts_opt \e__come_froms . JUMP_BACK
for_iter ::= GET_ITER . COME_FROM FOR_ITER
for_iter ::= GET_ITER . FOR_ITER
for_iter ::= GET_ITER FOR_ITER . 
forelsestmt ::= SETUP_LOOP . expr for_iter store for_block POP_BLOCK else_suite \e__come_froms
forelsestmt ::= SETUP_LOOP . expr for_iter store for_block POP_BLOCK else_suite _come_froms
forelsestmt ::= SETUP_LOOP expr . for_iter store for_block POP_BLOCK else_suite \e__come_froms
forelsestmt ::= SETUP_LOOP expr . for_iter store for_block POP_BLOCK else_suite _come_froms
forelsestmt ::= SETUP_LOOP expr for_iter . store for_block POP_BLOCK else_suite \e__come_froms
forelsestmt ::= SETUP_LOOP expr for_iter . store for_block POP_BLOCK else_suite _come_froms
forelsestmt ::= SETUP_LOOP expr for_iter store . for_block POP_BLOCK else_suite \e__come_froms
forelsestmt ::= SETUP_LOOP expr for_iter store . for_block POP_BLOCK else_suite _come_froms
genexpr_func ::= LOAD_FAST . FOR_ITER store comp_iter JUMP_BACK
get_iter ::= expr . GET_ITER
get_iter ::= expr GET_ITER . 
if_exp ::= expr . jmp_false expr JUMP_ABSOLUTE expr
if_exp ::= expr . jmp_false expr JUMP_FORWARD expr COME_FROM
if_exp ::= expr jmp_false . expr JUMP_ABSOLUTE expr
if_exp ::= expr jmp_false . expr JUMP_FORWARD expr COME_FROM
if_exp ::= expr jmp_false expr . JUMP_ABSOLUTE expr
if_exp ::= expr jmp_false expr . JUMP_FORWARD expr COME_FROM
if_exp_lambda ::= expr . jmp_false expr return_if_lambda return_stmt_lambda LAMBDA_MARKER
if_exp_lambda ::= expr jmp_false . expr return_if_lambda return_stmt_lambda LAMBDA_MARKER
if_exp_lambda ::= expr jmp_false expr . return_if_lambda return_stmt_lambda LAMBDA_MARKER
if_exp_not ::= expr . jmp_true expr _jump expr COME_FROM
if_exp_not_lambda ::= expr . jmp_true expr return_if_lambda return_stmt_lambda LAMBDA_MARKER
if_exp_true ::= expr . JUMP_FORWARD expr COME_FROM
ifelsestmt ::= testexpr . c_stmts_opt JUMP_FORWARD else_suite come_froms
ifelsestmt ::= testexpr \e_c_stmts_opt . JUMP_FORWARD else_suite come_froms
ifelsestmt ::= testexpr c_stmts_opt . JUMP_FORWARD else_suite come_froms
ifelsestmt ::= testexpr c_stmts_opt JUMP_FORWARD . else_suite come_froms
ifelsestmtc ::= testexpr . c_stmts_opt JUMP_ABSOLUTE else_suitec
ifelsestmtc ::= testexpr . c_stmts_opt JUMP_FORWARD else_suite come_froms
ifelsestmtc ::= testexpr \e_c_stmts_opt . JUMP_ABSOLUTE else_suitec
ifelsestmtc ::= testexpr \e_c_stmts_opt . JUMP_FORWARD else_suite come_froms
ifelsestmtc ::= testexpr c_stmts_opt . JUMP_ABSOLUTE else_suitec
ifelsestmtc ::= testexpr c_stmts_opt . JUMP_FORWARD else_suite come_froms
ifelsestmtc ::= testexpr c_stmts_opt JUMP_ABSOLUTE . else_suitec
ifelsestmtc ::= testexpr c_stmts_opt JUMP_ABSOLUTE else_suitec . 
ifelsestmtc ::= testexpr c_stmts_opt JUMP_FORWARD . else_suite come_froms
ifelsestmtl ::= testexpr . c_stmts_opt CONTINUE else_suitel
ifelsestmtl ::= testexpr . c_stmts_opt JUMP_BACK else_suitel
ifelsestmtl ::= testexpr \e_c_stmts_opt . CONTINUE else_suitel
ifelsestmtl ::= testexpr \e_c_stmts_opt . JUMP_BACK else_suitel
ifelsestmtl ::= testexpr \e_c_stmts_opt CONTINUE . else_suitel
ifelsestmtl ::= testexpr c_stmts_opt . CONTINUE else_suitel
ifelsestmtl ::= testexpr c_stmts_opt . JUMP_BACK else_suitel
ifelsestmtl ::= testexpr c_stmts_opt CONTINUE . else_suitel
ifelsestmtr ::= testexpr . return_if_stmts COME_FROM returns
iflaststmt ::= testexpr . c_stmts_opt JUMP_ABSOLUTE
iflaststmt ::= testexpr \e_c_stmts_opt . JUMP_ABSOLUTE
iflaststmt ::= testexpr c_stmts_opt . JUMP_ABSOLUTE
iflaststmt ::= testexpr c_stmts_opt JUMP_ABSOLUTE . 
iflaststmtl ::= testexpr . c_stmts
iflaststmtl ::= testexpr . c_stmts_opt JUMP_BACK
iflaststmtl ::= testexpr \e_c_stmts_opt . JUMP_BACK
iflaststmtl ::= testexpr c_stmts . 
iflaststmtl ::= testexpr c_stmts_opt . JUMP_BACK
ifstmt ::= testexpr . _ifstmts_jump
ifstmt ::= testexpr . return_if_stmts COME_FROM
ifstmt ::= testexpr . return_stmts COME_FROM
ifstmt ::= testexpr _ifstmts_jump . 
jmp_false ::= POP_JUMP_IF_FALSE . 
l_stmts ::= _stmts . 
l_stmts ::= _stmts . lastl_stmt
l_stmts ::= _stmts lastl_stmt . 
l_stmts ::= continues . 
l_stmts ::= lastl_stmt . 
l_stmts_opt ::= l_stmts . 
lastc_stmt ::= iflaststmt . 
lastl_stmt ::= iflaststmtl . 
lc_body ::= expr . LIST_APPEND
lc_body ::= expr LIST_APPEND . 
list ::= BUILD_LIST_0 . 
list ::= expr . BUILD_LIST_1
list ::= expr . expr BUILD_LIST_2
list ::= expr expr . BUILD_LIST_2
list_comp ::= BUILD_LIST_0 . list_iter
list_comp ::= BUILD_LIST_0 list_iter . 
list_for ::= expr . for_iter store list_iter JUMP_BACK
list_for ::= expr for_iter . store list_iter JUMP_BACK
list_for ::= expr for_iter store . list_iter JUMP_BACK
list_for ::= expr for_iter store list_iter . JUMP_BACK
list_for ::= expr for_iter store list_iter JUMP_BACK . 
list_if ::= expr . jmp_false list_iter
list_if_not ::= expr . jmp_true list_iter
list_iter ::= lc_body . 
list_iter ::= list_for . 
mkfunc ::= expr . LOAD_CODE MAKE_FUNCTION_1
mkfunc ::= expr . expr LOAD_CODE MAKE_FUNCTION_2
mkfunc ::= expr expr . LOAD_CODE MAKE_FUNCTION_2
mkfuncdeco ::= expr . mkfuncdeco CALL_FUNCTION_1
mkfuncdeco ::= expr . mkfuncdeco0 CALL_FUNCTION_1
print_items_nl_stmt ::= expr . PRINT_ITEM \e_print_items_opt PRINT_NEWLINE_CONT
print_items_nl_stmt ::= expr . PRINT_ITEM print_items_opt PRINT_NEWLINE_CONT
print_items_stmt ::= expr . PRINT_ITEM \e_print_items_opt
print_items_stmt ::= expr . PRINT_ITEM print_items_opt
print_nl_to ::= expr . PRINT_NEWLINE_TO
print_to ::= expr . print_to_items POP_TOP
print_to_nl ::= expr . print_to_items PRINT_NEWLINE_TO
raise_stmt1 ::= expr . RAISE_VARARGS_1
raise_stmt2 ::= expr . expr RAISE_VARARGS_2
raise_stmt2 ::= expr expr . RAISE_VARARGS_2
raise_stmt2 ::= expr expr RAISE_VARARGS_2 . 
raise_stmt3 ::= expr . expr expr RAISE_VARARGS_3
raise_stmt3 ::= expr expr . expr RAISE_VARARGS_3
raise_stmt3 ::= expr expr expr . RAISE_VARARGS_3
ret_and ::= expr . JUMP_IF_FALSE_OR_POP return_expr_or_cond COME_FROM
ret_or ::= expr . JUMP_IF_TRUE_OR_POP return_expr_or_cond COME_FROM
return ::= return_expr . RETURN_VALUE
return_expr ::= expr . 
return_expr_lambda ::= return_expr . RETURN_VALUE_LAMBDA
return_expr_lambda ::= return_expr . RETURN_VALUE_LAMBDA LAMBDA_MARKER
return_if_stmt ::= return_expr . RETURN_END_IF
return_if_stmts ::= _stmts . return_if_stmt
return_stmts ::= _stmts . return_stmt
returns ::= _stmts . return
slice0 ::= expr . DUP_TOP SLICE+0
slice0 ::= expr . SLICE+0
slice1 ::= expr . expr DUP_TOPX_2 SLICE+1
slice1 ::= expr . expr SLICE+1
slice1 ::= expr expr . DUP_TOPX_2 SLICE+1
slice1 ::= expr expr . SLICE+1
slice2 ::= expr . expr DUP_TOPX_2 SLICE+2
slice2 ::= expr . expr SLICE+2
slice2 ::= expr expr . DUP_TOPX_2 SLICE+2
slice2 ::= expr expr . SLICE+2
slice3 ::= expr . expr expr DUP_TOPX_3 SLICE+3
slice3 ::= expr . expr expr SLICE+3
slice3 ::= expr expr . expr DUP_TOPX_3 SLICE+3
slice3 ::= expr expr . expr SLICE+3
slice3 ::= expr expr expr . DUP_TOPX_3 SLICE+3
slice3 ::= expr expr expr . SLICE+3
sstmt ::= stmt . 
stmt ::= assign . 
stmt ::= call_stmt . 
stmt ::= continue . 
stmt ::= ifstmt . 
stmt ::= raise_stmt2 . 
stmts ::= sstmt . 
stmts ::= stmts . sstmt
stmts ::= stmts sstmt . 
store ::= STORE_FAST . 
store ::= expr . STORE_ATTR
store ::= expr . STORE_SLICE+0
store ::= expr . expr STORE_SLICE+1
store ::= expr . expr STORE_SLICE+2
store ::= expr . expr expr STORE_SLICE+3
store ::= expr expr . STORE_SLICE+1
store ::= expr expr . STORE_SLICE+2
store ::= expr expr . expr STORE_SLICE+3
store_subscript ::= expr . expr STORE_SUBSCR
store_subscript ::= expr expr . STORE_SUBSCR
subscript ::= expr . expr BINARY_SUBSCR
subscript ::= expr expr . BINARY_SUBSCR
subscript2 ::= expr . expr DUP_TOPX_2 BINARY_SUBSCR
subscript2 ::= expr expr . DUP_TOPX_2 BINARY_SUBSCR
testexpr ::= testfalse . 
testfalse ::= expr . jmp_false
testfalse ::= expr jmp_false . 
testtrue ::= expr . jmp_true
tuple ::= expr . BUILD_TUPLE_1
tuple ::= expr . expr BUILD_TUPLE_2
tuple ::= expr . expr expr expr expr BUILD_TUPLE_5
tuple ::= expr . expr expr expr expr expr BUILD_TUPLE_6
tuple ::= expr BUILD_TUPLE_1 . 
tuple ::= expr expr . BUILD_TUPLE_2
tuple ::= expr expr . expr expr expr BUILD_TUPLE_5
tuple ::= expr expr . expr expr expr expr BUILD_TUPLE_6
tuple ::= expr expr expr . expr expr BUILD_TUPLE_5
tuple ::= expr expr expr . expr expr expr BUILD_TUPLE_6
unary_convert ::= expr . UNARY_CONVERT
unary_not ::= expr . UNARY_NOT
unary_not ::= expr UNARY_NOT . 
unary_op ::= expr . unary_operator
while1elsestmt ::= SETUP_LOOP . l_stmts JUMP_BACK POP_BLOCK else_suitel COME_FROM
while1elsestmt ::= SETUP_LOOP . l_stmts JUMP_BACK else_suitel COME_FROM
while1stmt ::= SETUP_LOOP . l_stmts_opt CONTINUE COME_FROM
while1stmt ::= SETUP_LOOP . l_stmts_opt JUMP_BACK COME_FROM
while1stmt ::= SETUP_LOOP . l_stmts_opt JUMP_BACK POP_BLOCK COME_FROM
while1stmt ::= SETUP_LOOP . returns COME_FROM
while1stmt ::= SETUP_LOOP . returns pb_come_from
while1stmt ::= SETUP_LOOP \e_l_stmts_opt . CONTINUE COME_FROM
while1stmt ::= SETUP_LOOP \e_l_stmts_opt . JUMP_BACK COME_FROM
while1stmt ::= SETUP_LOOP \e_l_stmts_opt . JUMP_BACK POP_BLOCK COME_FROM
whileelsestmt ::= SETUP_LOOP . testexpr \e_l_stmts_opt JUMP_BACK POP_BLOCK else_suitel COME_FROM
whileelsestmt ::= SETUP_LOOP . testexpr l_stmts_opt JUMP_BACK POP_BLOCK else_suitel COME_FROM
whilestmt ::= SETUP_LOOP . testexpr \e_l_stmts_opt JUMP_BACK JUMP_BACK POP_BLOCK \e__come_froms
whilestmt ::= SETUP_LOOP . testexpr \e_l_stmts_opt JUMP_BACK JUMP_BACK POP_BLOCK _come_froms
whilestmt ::= SETUP_LOOP . testexpr \e_l_stmts_opt JUMP_BACK POP_BLOCK \e__come_froms
whilestmt ::= SETUP_LOOP . testexpr \e_l_stmts_opt JUMP_BACK POP_BLOCK _come_froms
whilestmt ::= SETUP_LOOP . testexpr l_stmts_opt JUMP_BACK JUMP_BACK POP_BLOCK \e__come_froms
whilestmt ::= SETUP_LOOP . testexpr l_stmts_opt JUMP_BACK JUMP_BACK POP_BLOCK _come_froms
whilestmt ::= SETUP_LOOP . testexpr l_stmts_opt JUMP_BACK POP_BLOCK \e__come_froms
whilestmt ::= SETUP_LOOP . testexpr l_stmts_opt JUMP_BACK POP_BLOCK _come_froms
whilestmt ::= SETUP_LOOP . testexpr returns \e__come_froms POP_BLOCK COME_FROM
whilestmt ::= SETUP_LOOP . testexpr returns _come_froms POP_BLOCK COME_FROM
with ::= expr . SETUP_WITH POP_TOP \e_suite_stmts_opt POP_BLOCK LOAD_CONST COME_FROM_WITH WITH_CLEANUP END_FINALLY
with ::= expr . SETUP_WITH POP_TOP suite_stmts_opt POP_BLOCK LOAD_CONST COME_FROM_WITH WITH_CLEANUP END_FINALLY
with_as ::= expr . SETUP_WITH store \e_suite_stmts_opt POP_BLOCK LOAD_CONST COME_FROM_WITH WITH_CLEANUP END_FINALLY
with_as ::= expr . SETUP_WITH store suite_stmts_opt POP_BLOCK LOAD_CONST COME_FROM_WITH WITH_CLEANUP END_FINALLY
yield ::= expr . YIELD_VALUE
Instruction context:
   
 L. 422       178  CONTINUE             69  'to 69'
->               181  JUMP_FORWARD          0  'to 184'
               184_0  COME_FROM           181  '181'

