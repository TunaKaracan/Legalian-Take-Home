CREATE TABLE IF NOT EXISTS nodes (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS edges (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    from_node_id INT UNSIGNED NOT NULL,
    to_node_id   INT UNSIGNED NOT NULL,

    PRIMARY KEY (id),

    CONSTRAINT fk_edges_from
        FOREIGN KEY (from_node_id)
        REFERENCES nodes(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_edges_to
        FOREIGN KEY (to_node_id)
        REFERENCES nodes(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_edges_from_node ON edges (from_node_id);
CREATE INDEX idx_edges_to_node ON edges (to_node_id)
