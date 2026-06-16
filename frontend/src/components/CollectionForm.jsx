/**
 * CollectionForm Component
 * Form for creating new collections
 */

import Button from "./Button";

export default function CollectionForm({ 
  collectionForm, 
  onChange, 
  onSubmit 
}) {
  return (
    <section className="card">
      <h2>Create Collection</h2>

      <form onSubmit={onSubmit} className="form">
        <label>
          Name
          <input
            name="name"
            value={collectionForm.name}
            onChange={onChange}
            required
          />
        </label>

        <label>
          Description
          <input
            name="description"
            value={collectionForm.description}
            onChange={onChange}
          />
        </label>

        <Button type="submit">Create Collection</Button>
      </form>
    </section>
  );
}
