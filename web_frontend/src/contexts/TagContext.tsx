import React, { createContext, useContext, useState, ReactNode } from 'react';

interface TagContextType {
  selectedTag: string | null;
  setSelectedTag: (tag: string | null) => void;
}

const TagContext = createContext<TagContextType | undefined>(undefined);

export function TagProvider({ children }: { children: ReactNode }) {
  const [selectedTag, setSelectedTag] = useState<string | null>(null);

  return (
    <TagContext.Provider value={{ selectedTag, setSelectedTag }}>
      {children}
    </TagContext.Provider>
  );
}

export function useTag() {
  const context = useContext(TagContext);
  if (context === undefined) {
    throw new Error('useTag must be used within a TagProvider');
  }
  return context;
}