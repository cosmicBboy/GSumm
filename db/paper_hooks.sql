CREATE TABLE `paper_hooks` (
  `title` VARCHAR(300) NOT NULL,
  `topic` text(45) NULL,
  `objectives` text(10000) NULL,
  `hypothesis` text(10000) NULL,
  `study_design` text(10000) NULL,
  `sampling_method` text(10000) NULL,
  `findings` text(10000) NULL,
  `implications` text(10000) NULL,
  `future_research` text(10000) NULL,
  `limitations` text(10000) NULL,
  PRIMARY KEY (`title`)
  );									