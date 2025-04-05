DELETE FROM sections;
DELETE FROM conditions;

INSERT INTO sections (label, name) VALUES
    ('vaatteet', 'farkut'),
    ('vaatteet', 'housut'),
    ('vaatteet', 'takit'),
    ('vaatteet', 'yläosat'),
    ('vaatteet', 'puvut'),
    ('kengät', 'sandaalit'),
    ('kengät', 'loaferit'),
    ('kengät', 'saappaat'),
    ('kengät', 'urheilukengät'),
    ('kengät', 'vapaa-ajan kengät'),
    ('asusteet', 'hatut'),
    ('asusteet', 'korut'),
    ('asusteet', 'laukut'),
    ('asusteet', 'vyöt'),
    ('asusteet', 'muut asusteet');

INSERT INTO conditions (name) VALUES
    ('uusi'),
    ('erinomainen'),
    ('hyvä'),
    ('kohtalainen'),
    ('heikko');