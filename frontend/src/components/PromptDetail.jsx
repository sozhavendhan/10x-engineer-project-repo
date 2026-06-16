/**
 * PromptDetail Component
 * Displays detailed view of a single prompt
 */

export default function PromptDetail({ prompt, collectionName }) {
  if (!prompt) return null;

  return (
    <div className="prompt-detail">
      <h2>{prompt.title}</h2>
      
      <div className="detail-section">
        <h3>Collection</h3>
        <p>{collectionName}</p>
      </div>

      <div className="detail-section">
        <h3>Description</h3>
        <p>{prompt.description || "No description provided."}</p>
      </div>

      <div className="detail-section">
        <h3>Content</h3>
        <pre>{prompt.content}</pre>
      </div>

      {prompt.tags && prompt.tags.length > 0 && (
        <div className="detail-section">
          <h3>Tags</h3>
          <div className="tags">
            {prompt.tags.map((tag) => (
              <span key={tag}>{tag}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
