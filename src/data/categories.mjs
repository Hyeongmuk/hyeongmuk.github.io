export const noteCategories = [
 { id:'qft', title:'Quantum Field Theory', summary:'Quantization and the geometric language of fields.' },
 { id:'mathematics', title:'Mathematics', summary:'Algebra, geometry, and categorical viewpoints.' },
 { id:'condensed', title:'Condensed Matter Physics', summary:'Quantum spin chains, topology, and many-body physics.' },
];
export const publicationCategories = [
 { id:'quantum-geometry', title:'Quantum Geometry' },
 { id:'band-topology', title:'Band Topology' },
 { id:'many-body-physics', title:'Many-Body Physics' },
];
export const slugArea = (area) => area?.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'') || 'other';
export const noteCategoryLabel = (id) => noteCategories.find(x=>x.id===id)?.title || id;
