--INICIO QUERY CONFIGURACION USUARIOS--
 
--Servicios
--1  SEGUÍ TUS RECLAMOS
--7  ENTERATE DE LAS NOVEDADES
--13  CUENTA CORRIENTE
--15  COMPRÁ NUESTROS PRODUCTOS
--16  CATÁLOGOS
--17  POST VENTA
--Servicios
 
insert into usuario_permisos_servicio (usuario_id, servicio_id, rol_id) values
(1,1,1),
(1,7,1),
(1,13,1),
(1,15,1),
(1,16,1),
(1,17,1);
 
select * from servicios_x_negocios sxn where servicio_id in (15,16,17);
 
select * from usuarios u WHERE user_name like '%003462.00%'
 
select * from razon_social rs where usuario_id =2024;
 
--select * from usuario_marca um where usuario_id = 1794
 
select * from usuario_negocio un where usuario_id = '1794'
 
select * from usuario_x_razon_social uxrs where razon_social_id = 540;
 
select * from usuario_permisos_servicio ups where usuario_id = '1794'
 
--select * from razon_social_x_marca rsxm where razon_social_id = '540'
 
select * from razon_social_x_negocio rsxn where razon_social_id = '540'
 
select * from razon_social_vendedores rsv where razon_social_id = '540'
 
--select * from negocio_marca nm where marca_id = '17'
 
select * from asesores_x_grupo;
 
select * from razon_social_asesores where razon_social_id=540; --asesor comercial (grupo comercial)
 
 
select * from razon_social_vendedores rsv ; -- vendedores del grupo de ventas
 
select * from asesor_cobranzas ac; --asesor cobranzas
 
select * from razon_social_asesores_cobranzas rsac
 
select * from vendedor v
 
select * from asesores order by asesor_id ;
 
select * from razon_social rs order by razon_social_id desc;
 
--FIN QUERY CONFIGURACION USUARIOS--