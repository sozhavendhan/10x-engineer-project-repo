/**
 * PromptCard Component
 * Displays a single prompt with its details and actions
 */

import Button from "./Button";

export default function PromptCard({ 
  prompt, 
  collectionName, 
  onEdit, 
  onDelete,
  onView
}) {
  return (
    <article className="prompt-card">
      <div className="prompt-card-header">
        <h3>{prompt.title}</h3>
        <span>{collectionName}</span>
      </div>

      <p className="description">
        {prompt.description || "No description provided."}
      </p>

      <pre>{prompt.content}</pre>

      {prompt.tags && prompt.tags.length > 0 && (
        <div className="tags">
          {prompt.tags.map((tag) => (
            <span key={tag}>{tag}</span>
          ))}
        </div>
      )}

      <div className="prompt-actions">
        {onView && (
          <Button 
            variant="secondary" 
            onClick={() => onView(prompt)}
          >
            View
          </Button>
        )}
        <Button 
          variant="secondary" 
          onClick={() => onEdit(prompt)}
        >
          Edit
        </Button>
        <Button 
          variant="danger" 
          onClick={() => onDelete(prompt.id)}
        >
          Delete
        </Button>
      </div>
    </article>
  );
}
