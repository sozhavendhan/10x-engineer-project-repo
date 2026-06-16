/**
 * PromptForm Component
 * Form for creating and editing prompts
 */

import Button from "./Button";

export default function PromptForm({ 
  promptForm, 
  collections, 
  isEditing, 
  onSubmit, 
  onChange, 
  onCancel 
}) {
  return (
    <section className="card">
      <h2>{isEditing ? "Edit Prompt" : "Create Prompt"}</h2>

      <form onSubmit={onSubmit} className="form">
        <label>
          Title
          <input
            name="title"
            value={promptForm.title}
            onChange={onChange}
            required
          />
        </label>

        <label>
          Content
          <textarea
            name="content"
            value={promptForm.content}
            onChange={onChange}
            rows="6"
            required
          />
        </label>

        <label>
          Description
          <input
            name="description"
            value={promptForm.description}
            onChange={onChange}
          />
        </label>

        <label>
          Collection
          <select
            name="collection_id"
            value={promptForm.collection_id}
            onChange={onChange}
          >
            <option value="">No collection</option>
            {collections.map((collection) => (
              <option key={collection.id} value={collection.id}>
                {collection.name}
              </option>
            ))}
          </select>
        </label>

        <label>
          Tags comma separated
          <input
            name="tags"
            value={promptForm.tags}
            onChange={onChange}
            placeholder="marketing, ai, summary"
          />
        </label>

        <div className="button-row">
          <Button type="submit">
            {isEditing ? "Update Prompt" : "Create Prompt"}
          </Button>

          {isEditing && (
            <Button 
              type="button" 
              variant="secondary"
              onClick={onCancel}
            >
              Cancel Edit
            </Button>
          )}
        </div>
      </form>
    </section>
  );
}
