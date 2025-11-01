-- Migrazione database per Rubrica Ministeriale
-- Aggiunge campi: livello, tempo_stimato, distrattori

-- Aggiungi colonna livello (BASE, INTERMEDIO, AVANZATO, DIFFICILE)
ALTER TABLE domande_verifica ADD COLUMN livello VARCHAR(20) DEFAULT 'BASE';

-- Aggiungi colonna tempo_stimato (tempo in minuti)
ALTER TABLE domande_verifica ADD COLUMN tempo_stimato INTEGER;

-- Aggiungi colonna distrattori (JSON con distrattori per livello INTERMEDIO)
ALTER TABLE domande_verifica ADD COLUMN distrattori TEXT;
