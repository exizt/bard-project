SET FOREIGN_KEY_CHECKS = 0;
drop table if exists section_article_rel;
drop table if exists section;
drop table if exists tag_article_rel;
drop table if exists tags;
drop table if exists article_content;
drop table if exists articles;
drop table if exists blog;

delete from django_content_type where id >= 7;
delete from django_migrations where id >= 19;
delete from auth_permission where id >= 25;
delete from django_admin_log;
SET FOREIGN_KEY_CHECKS = 1;