/**
 * PromptList Component
 * Displays a list/grid of all prompts
 */

import Button from "./Button";
import PromptCard from "./PromptCard";

export default function PromptList({ 
  prompts, 
  collections, 
  onEdit, 
  onDelete, 
  onView,
  onRefresh 
}) {
  function getCollectionName(collectionId) {
    const collection = collections.find((item) => item.id === collectionId);
    return collection ? collection.name : "No collection";
  }

  return (
    <section className="card full-width">
      <div className="section-heading">
        <div>
          <h2>Prompt List</h2>
          <p className="muted">{prompts.length} prompt(s) available</p>
        </div>
        <Button variant="secondary" onClick={onRefresh}>
          Refresh
        </Button>
      </div>

      {prompts.length === 0 ? (
        <p className="muted">No prompts found. Create your first prompt above.</p>
      ) : (
        <div className="prompt-grid">
          {prompts.map((prompt) => (
            <PromptCard
              key={prompt.id}
              prompt={prompt}
              collectionName={getCollectionName(prompt.collection_id)}
              onEdit={onEdit}
              onDelete={onDelete}
              onView={onView}
            />
          ))}
        </div>
      )}
    </section>
  );
}
