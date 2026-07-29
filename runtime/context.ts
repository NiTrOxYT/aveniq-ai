/**
 * AVENIQ AI — Context Propagation & Template Interpolation Engine
 * Interpolates variables like {{ research.output }} and {{ variables.myVar }} in prompts.
 */

export class ContextInterpolator {
  public static interpolate(
    template: string,
    outputs: Map<string, any>,
    globalVariables: Record<string, any> = {}
  ): string {
    if (!template) return '';

    return template.replace(/\{\{\s*([a-zA-Z0-9_\.]+)\s*\}\}/g, (match, pathStr) => {
      const parts = pathStr.split('.');
      const rootKey = parts[0];

      let value: any;
      if (rootKey === 'variables') {
        value = globalVariables[parts[1]];
      } else if (outputs.has(rootKey)) {
        value = outputs.get(rootKey);
        if (parts.length > 1) {
          for (let i = 1; i < parts.length; i++) {
            if (value && typeof value === 'object') {
              value = value[parts[i]];
            } else {
              value = undefined;
              break;
            }
          }
        }
      }

      if (value === undefined || value === null) {
        return match; // Keep placeholder if unresolved
      }

      if (typeof value === 'object') {
        return JSON.stringify(value, null, 2);
      }

      return String(value);
    });
  }
}
