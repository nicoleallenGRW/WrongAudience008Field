SELECT 
  call.index_entry as "call number",
  control.p22, 
  title.material_code,
  bib.record_num, 
  bib.title
  
  
FROM 
sierra_view.control_field AS control 
JOIN sierra_view.bib_view AS BIB ON BIB.id = control.record_id 
JOIN sierra_view.phrase_entry AS call on BIB.id = call.record_id
JOIN sierra_view.bib_record_property as title on call.record_id = title.bib_record_id



WHERE 


call.varfield_type_code = 'c' 
and control.p22 != 'e'  
and (call.index_entry like 'LT %' or call.index_entry like 'Fiction %' 
or call.index_entry like 'Mystery %'or call.index_entry like 'graphic %'or call.index_entry like 'game %'or call.index_entry like 'dvd %'
or call.index_entry like 'Comp %'or call.index_entry like 'JPN %'or call.index_entry like 'SPA %'or call.index_entry like 'REF %'
or call.index_entry like 'ita %'or call.index_entry like 'scifi %'or call.index_entry like 'PBK %'or call.index_entry like 'chi %'
or call.index_entry like '0%' or call.index_entry like '1%' or call.index_entry like '2%' or call.index_entry like '3%' or call.index_entry like '4%' or call.index_entry like '5%'
or call.index_entry like '6%' or call.index_entry like '7%' or call.index_entry like '8%' or call.index_entry like '9%')
and control.control_num = '8' 
and title.material_code != '@' and title.material_code != 'e' and title.material_code != 'o' and title.material_code != 't' 
and bib.bcode3 = '-'



 order by
 call.index_entry;