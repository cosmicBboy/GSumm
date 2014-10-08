CREATE TABLE `paper_metadata` (
  `id` VARCHAR(45) NOT NULL,
  `author` VARCHAR(45) NULL,
  `publication_date` VARCHAR(45) NULL,
  `journal` VARCHAR(45) NULL,
  `article_type` VARCHAR(45) NULL,
  `subject` VARCHAR(45) NULL,
  `subject_level_1` VARCHAR(45) NULL,
  `eissn` VARCHAR(45) NULL,
  `publisher` VARCHAR(45) NULL,
  PRIMARY KEY (`id`)
  );