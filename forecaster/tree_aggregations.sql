--aggregate on product level and channel level

select 	
	"ud".cn_id, 
	sum("ud".quantity), 
	"ud".date 
from upds_details as "ud" 
join view_channels_tree as "vc" on "vc".c2_id="ud".channel_id 
join view_products_tree as "vp" on "vp".c3_id="ud".product_id
where "vc".cn_id=cn_id and "vp".pn_id=pn_id
group by 
	"ud".channel_id, 
	"ud".date 
order by 
	"ud".channel_id, 
	"ud".date;
	
	
--select products of level 1
select
	description,
	id
from products
where level=1;

--select channels of level 1
select
	description,
	id
from channels
where level=1;
	
--select products of parent id = pid
select
	description,
	id
from products
where parent_id=p_id;

--select channels of parent_id = cid
select
	description,
	id
from channels
where parent_id = c_id;

select 	
	"ud".cn_id, 
	sum("ud".quantity), 
	"ud".date 
from upds_details as "ud" 
join view_channels_tree as "vc" on "vc".c2_id="ud".channel_id 
join view_products_tree as "vp" on "vp".c3_id="ud".product_id
where "vc".cn_id=cn_id and "vp".pn_id=pn_id
group by 
	"ud".channel_id, 
	"ud".date 
order by 
	"ud".channel_id, 
	"ud".date;
	
select 'ped'||'01/04/2018', '01/04/2018', '01/04/2018', p1, p2, p3, p4, 0, 'TOTAL', 'INTERNO', 'RETAIL/DISTRIB/KA', '43708379006485', null  from temp_file_new_prd;

INSERT INTO temp_file_new_fat (pedido, p1, p2, p3, p4, c1, c2, c3, c4, quant, dat)
	SELECT 
		"ped".pedido,
		"ped".p1,
		"ped".p2,
		"ped".p3,
		"ped".p4,
		"ped".c1,
		"ped".c2,
		"ped".c3,
		"ped".c4,
		"ped".quant,
		"ped".dat_p
	FROM temp_file_new_ped AS "ped";
UPDATE temp_file_new_fat SET nf = concat('nf',pedido::text);
UPDATE temp_file_new_fat SET sts = null;



            select 	
				*
            from upds_details as "ud" 
            join view_channels_tree as "vc" on "vc".c2_id="ud".channel_id 
            join view_products_tree as "vp" on "vp".p3_id="ud".product_id
            where "vc".c2_id='4' and "vp".p2_id='13';
			
	select 	
    *
	from upds_details as "ud" 
    join (select c2_id from view_channels_tree where c2_id='4') as "vc" on "vc".c2_id="ud".channel_id 
    join (select p3_id from view_products_tree where p2_id='13') as "vp" on "vp".p3_id="ud".product_id;

	select distinct on (p2_id, p3_id) p2_id, p3_id from view_products_tree where p2_id='8'
	select distinct on (c2_id, c3_id) c2_id, c3_id from view_channels_tree where c2_id='13'
	
	select 	
        "vp".p2_id,
        "vc".c2_id, 
        sum("ud".quantity), 
        "ud".date 
    from upds_details as "ud" 
    join (select distinct on (c2_id, c3_id) c2_id, c3_id from view_channels_tree where c2_id='4') as "vc" on "vc".c2_id="ud".channel_id 
    join  (select distinct on (p2_id, p3_id) p2_id, p3_id from view_products_tree where p2_id='8') as "vp" on "vp".p3_id="ud".product_id
    group by 
        "vp".p2_id,
        "vc".c2_id, 
        "ud".date 
    order by 
        "vp".p2_id,
        "vc".c2_id, 
        "ud".date;

		
    select 	
        "vp".p2_id,
        "vc".c2_id, 
        sum("ud".quantity), 
        "ud".date 
    from upds_details as "ud" 
    join (select distinct on (c2_id, c2_id) c2_id, c2_id from view_channels_tree where c2_id='4') as "vc" on "vc".c2_id="ud".channel_id 
    join  (select distinct on (p3_id, p2_id) p3_id, p2_id from view_products_tree where p2_id='8') as "vp" on "vp".p3_id="ud".product_id
    group by 
        "vp".p2_id,
        "vc".c2_id, 
        "ud".date 
    order by 
        "vp".p2_id,
        "vc".c2_id, 
        "ud".date;

UPDATE new_products_tree set strt_at = 'MTO';
UPDATE new_products_tree set u_med = 'QTD';
UPDATE new_products_tree set u_conv = null;
UPDATE new_products_tree set ftr = 1;
UPDATE new_products_tree set strt_aqui = 'C';


