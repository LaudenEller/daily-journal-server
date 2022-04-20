CREATE TABLE journal_entries (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
concept VARCHAR(50) NOT NULL,
entry VARCHAR(250) NOT NULL,
moodId INT NOT NULL,
date CURRENT_DATE,
FOREIGN KEY('moodId') REFERENCES 'Table'('mood')
);

CREATE TABLE moods (
id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
label VARCHAR(50)
);

CREATE TABLE `Tag` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name` VARCHAR NOT NULL
    );

CREATE TABLE `Entrytag` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `entry_id` INTEGER NOT NULL,
    `tag_id` INTEGER NOT NULL,
    FOREIGN KEY (`entry_id`) REFERENCES `journal_entries`(`id`),
    FOREIGN KEY (`tag_id`) REFERENCES `Tag`(`id`)
    );

INSERT INTO `Tag` VALUES (null, "DELETE");

UPDATE `Tag`
SET name = 'GET'
WHERE name == 'CREATE'

DROP TABLE journal_entries

INSERT INTO moods(id, label) VALUES (4, 'Ok');

INSERT INTO journal_entries(id, concept, entry, moodId, date) VALUES (null, 'Python', 'I learned about classes', 4, '20220415');

UPDATE moods SET id = 2
WHERE id IS NULL

SELECT *
FROM journal_entries

ALTER TABLE journal_entries
RENAME COLUMN mood_id TO moodId;

SELECT
                e.id,
                e.concept,
                e.entry,
                e.moodId,
                e.date,
                m.label,
                t.name
            FROM journal_entries e
            LEFT JOIN Moods m
            ON m.id = e.moodId
            LEFT JOIN Entrytag et
            ON et.entry_id = e.id
            LEFT JOIN Tag t
            ON et.tag_id = t.id
SELECT
                                t.id,
                                t.name tag_name
                            FROM journal_entries e
                            JOIN Entrytag et
                            ON et.entry_id = e.id
                            LEFT JOIN Tag t
                            ON et.tag_id = t.id
                            WHERE et.entry_id = 6