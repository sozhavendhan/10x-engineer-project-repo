/**
 * CollectionList Component
 * Displays the list of collections with actions
 */

import Button from "./Button";

export default function CollectionList({ collections, onDelete }) {
  return (
    <div className="collection-list">
      <h3>Collections</h3>
      {collections.length === 0 ? (
        <p className="muted">No collections yet.</p>
      ) : (
        collections.map((collection) => (
          <div key={collection.id} className="collection-item">
            <div>
              <strong>{collection.name}</strong>
              <span>{collection.description || "No description"}</span>
            </div>
            {onDelete && (
              <Button
                variant="danger"
                onClick={() => onDelete(collection.id)}
                style={{ fontSize: "0.875rem", padding: "0.25rem 0.5rem" }}
              >
                Delete
              </Button>
            )}
          </div>
        ))
      )}
    </div>
  );
}
