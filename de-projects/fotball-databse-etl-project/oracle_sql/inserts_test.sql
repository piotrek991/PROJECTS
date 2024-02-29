create table accounts (
  account_id integer
    generated as identity
    not null
    primary key,
  username varchar2(10)
    not null
    unique,
  given_name varchar2(512)
    not null
);

exec dbms_errlog.create_error_log ( 'raw_footballers_data' );

INSERT ALL
into accounts ( username, given_name ) values ( 'chrissaxon', 'Christopher' )
    log errors into err$_accounts ('load failed') reject limit unlimited
into accounts ( username, given_name ) values ( 'chrissaxon', 'Christopher' )
    log errors into err$_accounts ('load1') reject limit unlimited  
into accounts ( username, given_name ) values ( 'chrissaxon', 'Christopher' )
    log errors into err$_accounts ('load1') reject limit unlimited
into accounts ( username, given_name ) values ( 'chrissaxon', 'Christopher' )
  log errors into err$_accounts ('load1') reject limit unlimited
  SELECT 1 FROM DUAL;
  
  
select * from err$_accounts


select * from all_tables
where table_name like 'err%';
