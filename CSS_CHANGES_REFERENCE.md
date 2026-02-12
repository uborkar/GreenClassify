# Quick CSS Changes Reference

## CSS Variables Updated (Root)

```css
/* OLD VALUES */
--primary-color: #1a5e3f;
--primary-dark: #0f3d28;
--primary-light: #2a7a52;
--secondary-color: #4CAF50;
--accent-color: #66BB6A;
--green-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);

/* NEW VALUES */
--primary-color: #6366f1;
--primary-dark: #4338ca;
--primary-light: #818cf8;
--secondary-color: #8b5cf6;
--accent-color: #ec4899;
--purple-gradient: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
--blue-gradient: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
```

## Key Component Changes

### Navbar
- Background: `rgba(15, 61, 40, 0.98)` → `linear-gradient(135deg, #4338ca 0%, #6366f1 100%)`
- Border bottom: Green tint → Purple tint
- Hover background: `rgba(102, 187, 106, 0.15)` → `rgba(139, 92, 246, 0.2)`

### About Section
- Background: `linear-gradient(135deg, #1a5e3f 0%, #0f3d28 100%)` → `linear-gradient(135deg, #4338ca 0%, #6366f1 100%)`

### Feature Cards
- Icon gradient: `var(--green-gradient)` → `var(--purple-gradient)`
- Hover border: `rgba(102, 187, 106, 0.3)` → `rgba(139, 92, 246, 0.4)`

### Buttons & Upload
- All gradients: `var(--green-gradient)` → `var(--purple-gradient)`
- Shadows: Green-tinted → Purple-tinted

### Footer
- Background: `linear-gradient(135deg, #0f3d28 0%, #1a5e3f 100%)` → `linear-gradient(135deg, #4338ca 0%, #6366f1 100%)`

## Files Modified
- `d:\MajorProjects\greenclassify\flask\static\css\style.css`

Total lines modified: ~50+ CSS properties updated across the entire stylesheet
