CREATE TABLE IF NOT EXISTS edges (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    from_node_id INT UNSIGNED NOT NULL,
    to_node_id   INT UNSIGNED NOT NULL,

    PRIMARY KEY (id),

    KEY idx_edges_from_node (from_node_id),
    KEY idx_edges_to_node   (to_node_id),

    CONSTRAINT fk_edges_from
        FOREIGN KEY (from_node_id)
        REFERENCES nodes(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_edges_to
        FOREIGN KEY (to_node_id)
        REFERENCES nodes(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;