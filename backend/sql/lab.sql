create table if not exists user
(
    email           varchar(255) not null,
    id              char(32)     not null
        primary key,
    hashed_password varchar(255) not null,
    is_superuser    tinyint(1)   not null,
    username        varchar(255) null,
    avatar          varchar(255) null,
    dept            varchar(255) null
);

create table if not exists blogpost
(
    title          varchar(255)                                      not null,
    category       enum ('TECH', 'LIFE', 'STUDY', 'TRAVEL', 'OTHER') not null,
    summary        varchar(500)                                      not null,
    content        varchar(255)                                      not null,
    allow_comments tinyint(1)                                        not null,
    featured       tinyint(1)                                        not null,
    id             char(32)                                          not null
        primary key,
    author_id      char(32)                                          not null,
    status         enum ('DRAFT', 'PUBLISHED')                       not null,
    tags           json                                              null,
    created_at     datetime                                          not null,
    updated_at     datetime                                          not null,
    published_at   datetime                                          null,
    views_count    int                                               not null,
    likes_count    int                                               not null,
    comments_count int                                               not null,
    constraint blogpost_ibfk_1
        foreign key (author_id) references user (id)
);

create table if not exists blogimage
(
    id         char(32)     not null
        primary key,
    blog_id    char(32)     not null,
    image_url  varchar(255) not null,
    created_at datetime     not null,
    constraint blogimage_ibfk_1
        foreign key (blog_id) references blogpost (id)
);

create index blog_id
    on blogimage (blog_id);

create index author_id
    on blogpost (author_id);

create table if not exists comment
(
    id          char(32)     not null
        primary key,
    post_id     char(32)     not null,
    user_id     char(32)     not null,
    parent_id   char(32)     null,
    content     varchar(255) not null,
    created_at  datetime     not null,
    updated_at  datetime     not null,
    likes_count int          not null,
    constraint comment_ibfk_1
        foreign key (post_id) references blogpost (id),
    constraint comment_ibfk_2
        foreign key (user_id) references user (id),
    constraint comment_ibfk_3
        foreign key (parent_id) references comment (id)
);

create index parent_id
    on comment (parent_id);

create index post_id
    on comment (post_id);

create index user_id
    on comment (user_id);

create table if not exists commentlike
(
    id         char(32) not null
        primary key,
    comment_id char(32) not null,
    user_id    char(32) not null,
    created_at datetime not null,
    constraint commentlike_ibfk_1
        foreign key (comment_id) references comment (id),
    constraint commentlike_ibfk_2
        foreign key (user_id) references user (id)
);

create index comment_id
    on commentlike (comment_id);

create index user_id
    on commentlike (user_id);

create table if not exists lostitem
(
    type          enum ('LOST', 'FOUND')                                     not null,
    title         varchar(255)                                               not null,
    category      enum ('CARD', 'ELECTRONICS', 'BOOKS', 'CLOTHING', 'OTHER') not null,
    description   varchar(2000)                                              not null,
    location      varchar(255)                                               not null,
    time          datetime                                                   not null,
    contact_type  enum ('PHONE', 'WECHAT', 'QQ')                             not null,
    contact_value varchar(255)                                               null,
    hide_contact  tinyint(1)                                                 not null,
    id            char(32)                                                   not null
        primary key,
    owner_id      char(32)                                                   not null,
    status        enum ('UNCLAIMED', 'CLAIMED', 'EXPIRED')                   not null,
    created_at    datetime                                                   not null,
    updated_at    datetime                                                   not null,
    views_count   int                                                        not null,
    lat           float                                                      null comment '纬度',
    lng           float                                                      null comment '经度',
    constraint lostitem_ibfk_1
        foreign key (owner_id) references user (id)
);

create table if not exists itemimage
(
    id         char(32)     not null
        primary key,
    item_id    char(32)     not null,
    image_url  varchar(255) not null,
    created_at datetime     not null,
    constraint itemimage_ibfk_1
        foreign key (item_id) references lostitem (id)
);

create index item_id
    on itemimage (item_id);

create index owner_id
    on lostitem (owner_id);

create table if not exists notification
(
    id         char(32)     not null
        primary key,
    user_id    char(32)     not null,
    content    varchar(255) not null,
    is_read    tinyint(1)   not null,
    created_at datetime     not null,
    constraint notification_ibfk_1
        foreign key (user_id) references user (id)
);

create index user_id
    on notification (user_id);

create table if not exists postlike
(
    id         char(32) not null
        primary key,
    post_id    char(32) not null,
    user_id    char(32) not null,
    created_at datetime not null,
    constraint postlike_ibfk_1
        foreign key (post_id) references blogpost (id),
    constraint postlike_ibfk_2
        foreign key (user_id) references user (id)
);

create index post_id
    on postlike (post_id);

create index user_id
    on postlike (user_id);

create table if not exists report
(
    id          char(32)     not null
        primary key,
    reporter_id char(32)     not null,
    target_type varchar(255) not null,
    target_id   char(32)     not null,
    reason      varchar(255) not null,
    created_at  datetime     not null,
    constraint report_ibfk_1
        foreign key (reporter_id) references user (id)
);

create index reporter_id
    on report (reporter_id);

